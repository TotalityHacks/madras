'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('reader_reader_hackathons', {
    'reader_id': {
      type: DataTypes.INTEGER,
    },
    'hackathon_id': {
      type: DataTypes.INTEGER,
    },
  }, {
    tableName: 'reader_reader_hackathons',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

