'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('director_hackathon', {
    'name': {
      type: DataTypes.STRING,
    },
    'organization_id': {
      type: DataTypes.INTEGER,
    },
  }, {
    tableName: 'director_hackathon',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

