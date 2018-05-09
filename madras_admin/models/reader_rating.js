'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('reader_rating', {
    'application_id': {
      type: DataTypes.INTEGER,
    },
  }, {
    tableName: 'reader_rating',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

